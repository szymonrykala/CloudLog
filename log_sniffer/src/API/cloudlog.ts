import Log, { Type } from "../models/Log";
import { AWSGatewayService, RequestMethod } from "./base";
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

        if (process.env.NODE_ENV === "development" || this.credentialsAreDemo()) {
            return mockedLogs
        }

        const logs = this.signedFetch({
            method: RequestMethod.GET,
            endpoint: "/dev/logs",
            query: query
        })
        return logs
    }
};
