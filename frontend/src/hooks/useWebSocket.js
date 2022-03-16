import { useState, useEffect, useRef, useCallback  } from "react";


export const useWebSocket = (url) => {
	const [isPaused, setIsPaused] = useState(false);
	const [data, setData] = useState()
	const [status, setStatus] = useState(false);
	const ws = useRef(null);

	useEffect(() => {
		if (!isPaused) {
			ws.current = new WebSocket(url)

			ws.current.onopen = () => setStatus(true)
			ws.current.onclose = () => setStatus(false)

			gettingData();
		}

		return () => ws.current.close();
	}, [ws, isPaused, url]);

	const gettingData = useCallback(() => {
		if (!ws.current) return;

		ws.current.onmessage = e => {
			if (isPaused) return;

			const message = JSON.parse(e.data);
			setData(message)
		};
	}, [isPaused] )

	return {
		"isPaused": isPaused,
		"setIsPaused": setIsPaused,
		"data": data,
		"status": status,
		"ws": ws
	}
}
