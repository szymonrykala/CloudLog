import { useCallback, useEffect, useState } from "react";
import { GetLogsQueryParams, GetLogsResponse } from "./cloudlog";
import { CloudLogService } from "./cloudlog";


const CLService = new CloudLogService()


export function useCloudLogGetLogs(params: GetLogsQueryParams) {
    const [logs, setLogs] = useState<GetLogsResponse>([])
    const [err, setErr] = useState<string>("")

    const fetchLogs = useCallback(async () => {
        try {
            const data = await CLService.getLogs(params)

            setLogs(data.sort((a,b)=> b.timestamp - a.timestamp))
            setErr("")
        } catch (e: any) {
            console.error(e)
            setErr(e.message)
        }
    }, [params, setErr])


    useEffect(() => {
        fetchLogs()
        return () => {
            setLogs([]); setErr("");
        }
    }, [
        fetchLogs,
        setErr
    ])

    return { logs, err }
}