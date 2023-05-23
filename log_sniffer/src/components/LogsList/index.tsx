import { List, ListItem, ListItemContent, Typography } from "@mui/joy";
import LogListItem from "./LogListItem";
import { useCloudLogGetLogs } from "../../API/hooks";
import { useQueryParamsContext } from "../QueryParams/context";
import { GetLogsQueryParams } from "../../API/cloudlog";
import ErrorBanner from "../ErrorBanner";


function Empty() {
    return <ListItem>
        <ListItemContent>
            <Typography textAlign="center">
                No logs found for given parameters 🫢
            </Typography>
        </ListItemContent>
    </ListItem>
}



export default function LogsList() {
    const paramsCtx = useQueryParamsContext<GetLogsQueryParams>()
    const { logs, err } = useCloudLogGetLogs(paramsCtx.params)

    return (
        <>
            <ErrorBanner message={err} />
            <List sx={{ 
                width: "100%", 
                gap: 1 
            }}>
                {
                    logs.length ? logs.map(log => <LogListItem key={log.id} log={log} />) : <Empty />
                }
            </List>
        </>
    );
}