import { useState, useContext, useEffect } from "react";

import AuthContext from "../context/AuthContext";


export const useFetch = (url) => {
    const [fetchData, setFetchData] = useState()
    const { authTokens, logoutUser } = useContext(AuthContext)

    useEffect(()=>{
        const fetchList = async () => {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + String(authTokens.access),
                },
            });
        
            const data = await response.json();
        
            if (response.status === 200) {
                setFetchData(data);
            } else if (response.statusText === "Unauthorized") {
                logoutUser();
            }
        }

        fetchList()
    }, [])

    return {
        'fetchData': fetchData
    }
};