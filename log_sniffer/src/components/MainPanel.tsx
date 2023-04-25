import Stack from "@mui/joy/Stack/Stack";
import QueryParamsContextProvider from "./QueryParams/context";
import { GetLogsQueryParams } from "../API/cloudlog";
import ParameterPanel from "./QueryParams/ParameterPanel";
import LogsList from "./LogsList";


const queryParamsDefaults: GetLogsQueryParams = {
    fromDate: new Date(Date.now()).toISOString(),
    toDate: new Date(Date.now() - (60 * 60 * 24 * 1)).toISOString(),
    severity: 7,
}


export default function MainPanel(){
    return (
        <QueryParamsContextProvider<GetLogsQueryParams> defaults={queryParamsDefaults}>
            <Stack spacing={2} >
                <ParameterPanel/>
                <LogsList/>
            </Stack>
        </QueryParamsContextProvider>
    )
}