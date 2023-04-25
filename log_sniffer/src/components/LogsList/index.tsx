import { List } from "@mui/joy";
import LogListItem from "./LogListItem";
import { useCloudLogGetLogs } from "../../API/hooks";
import { useQueryParamsContext } from "../QueryParams/context";
import { GetLogsQueryParams } from "../../API/cloudlog";



export default function LogsList() {
    const paramsCtx = useQueryParamsContext<GetLogsQueryParams>()
    const logs = useCloudLogGetLogs(paramsCtx.params)

    return (
        <List sx={{ width: "100%", gap: 1 }}>
            {
                logs.map(log => <LogListItem key={log.id} log={log} />)
            }
        </List>
    );
}