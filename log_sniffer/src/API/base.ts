import { HttpRequest } from '@aws-sdk/protocol-http';
import { SignatureV4 } from '@aws-sdk/signature-v4';
import { Sha256 } from '@aws-crypto/sha256-js';
import { Headers } from 'node-fetch';


export enum RequestMethod {
    GET = "GET",
    PATCH = "PATCH"
}


export interface ServiceFetchParams {
    endpoint: string
    method: RequestMethod
    headers?: any
    body?: object
    query: URLSearchParams
}

export interface APISericeFetch {
    method: RequestMethod
    headers: Headers,
    body?: string
}

export class APIServiceException extends Error {
}


export abstract class APIService {
    protected BASE_URL: string = process.env.REACT_APP_API_URL as string

    protected async fetch(url: string, params: APISericeFetch) {
        let data: any
        let resp: any

        try {
            resp = await fetch(url,
                {
                    credentials: "omit",
                    ...params
                }
            )
            data = await resp.json()
        } catch (error) {
            throw new APIServiceException(this.parseStatusCode(403))
        }

        if (resp?.ok) {
            return data
        }

        console.error(data?.message)
        throw new APIServiceException(this.parseStatusCode(resp.status))
    }

    private parseStatusCode(status: number): string {
        switch (status) {
            case 400:
                return "Data You provided are not correct 🤔";

            case 401:
            case 403:
                return "Credentials You provided are invalid 🔑"

            default:
                return "Someting wrong happened 🫣 - we will fix it 🤥."
        }
    }
}


export const ACCESS_KEY = "wfset5fw54fr";
export const SECRET_KEY = "fvfdjnoiuj98we";


export abstract class AWSGatewayService extends APIService {
    private API_REGION = process.env.REACT_APP_API_REGION as string
    private accessKey: string;
    private secretKey: string;

    constructor() {
        super()
        this.accessKey = localStorage.getItem(ACCESS_KEY) || "none";
        this.secretKey = localStorage.getItem(SECRET_KEY) || "none";
    }

    public static saveCredentials(secretKey: string, secretValue: string) {
        localStorage.setItem(ACCESS_KEY, secretKey)
        localStorage.setItem(SECRET_KEY, secretValue)
    }


    private async signRequest(config: HttpRequest) {
        const credentials = {
            accessKeyId: this.accessKey,
            secretAccessKey: this.secretKey,
        }

        const sigv4 = new SignatureV4({
            service: 'execute-api',
            region: this.API_REGION,
            credentials,
            sha256: Sha256,
        })
        return sigv4.sign(config as HttpRequest)
    }


    protected async signedFetch(params: ServiceFetchParams): Promise<any> {

        const querystring = params.query.toString()
        const url = `${params.endpoint}?${querystring}`
        const hostname = new URL(this.BASE_URL + url).hostname


        const config: Omit<Omit<HttpRequest, 'protocol'>, 'clone'> = {
            method: params.method,
            hostname: this.BASE_URL,
            path: params.endpoint,
            headers: {
                "Accept": 'application/json',
                "host": hostname,
                'Content-Type': 'application/json',
            },
            query: Object.fromEntries(params.query.entries())
        }

        const signedRequest = await this.signRequest(config as HttpRequest)


        return super.fetch(
            this.BASE_URL + url,
            {
                method: signedRequest.method as RequestMethod.GET,
                headers: signedRequest.headers as any as Headers
            }
        )
    }

}
