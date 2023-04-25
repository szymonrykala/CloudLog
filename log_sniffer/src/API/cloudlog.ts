import Log, { Type } from "../models/Log";
import { AWSGatewayService } from "./base";
import { mockedLogs } from "./mockdata";


export interface GetLogsQueryParams {
    fromDate?: string
    toDate?: string
    severity?: number
    type?: Type
    hostname?: string
    unit?: string
};


export type GetLogsResponse = Log[];


export class CloudLogService extends AWSGatewayService {

    public async getLogs(params: GetLogsQueryParams): Promise<GetLogsResponse> {
        const query = new URLSearchParams(Object.entries(params))
        console.debug(query.toString())

        const logs = await super.fetch({
            method: "GET",
            endpoint: `/logs?${query.toString()}`
        })
        // return logs as GetLogsResponse
        // console.log()

        return mockedLogs
    }
};

// const CloudLogService = new AWSCloudLogService()
// export default  CloudLogService