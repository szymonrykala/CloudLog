import { useCallback, useEffect, useState } from "react";
import { GetLogsQueryParams, GetLogsResponse } from "./cloudlog";
import { CloudLogService } from "./cloudlog";


const CLService = new CloudLogService()


export function useCloudLogGetLogs(params: GetLogsQueryParams) {
    const [logs, setLogs] = useState<GetLogsResponse>([])

    const fetchLogs = useCallback(async () => {
        const data = await CLService.getLogs(params)
        console.debug(data)
        setLogs(data)
    },[params])

    useEffect(() => {
        fetchLogs()
        return ()=> setLogs([])
    }, [
        fetchLogs
    ])

    return logs
}