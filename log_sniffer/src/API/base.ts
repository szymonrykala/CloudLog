import { HttpRequest } from '@aws-sdk/protocol-http';
import { SignatureV4 } from '@aws-sdk/signature-v4';
import { fromUtf8 } from '@aws-sdk/util-utf8-browser';
import { Sha256 } from '@aws-crypto/sha256-js';
// import { HttpRequest } from '@aws-sdk/protocol-http/dist-types/httpRequest';

export interface ServiceFetchParams {
    endpoint: string
    method: string
    headers?: object
    body?: object
}


export class APIServiceException extends Error {
    // constructor(message: string) {
    //     super(message)
    //     // this.message = message
    // }
}


export abstract class APIService {
    protected BASE_URL: string = process.env.REACT_APP_API_URL as string

    protected async fetch(params: ServiceFetchParams) {
        const resp = await fetch(
            this.BASE_URL + params.endpoint,
            {
                method: params.method,
                cache: 'no-cache',
                mode: 'cors',
                headers: {
                    ...params.headers,
                    "User-Agent": process.env?.REACT_APP_NAME as string || "React API Service",
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(params.body)
            }
        )

        let data: any
        try {
            data = await resp.json()
            if (resp.ok) {
                return data
            }
        } catch (error) {
            console.error(error)
            throw new APIServiceException("Someting happened with server response 😲.")
        }

        throw new APIServiceException(data?.message || "I'm sorry 😥,\nSomething wrong happened.")
    }

}


export const ACCESS_KEY = "wfset5fw54fr";
export const SECRET_KEY = "fvfdjnoiuj98we";


export abstract class AWSGatewayService extends APIService {
    private API_REGION = "eu-central-1"
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

    private async genAWSSig4(params: ServiceFetchParams): Promise<HttpRequest> {
        const request: HttpRequest = new HttpRequest(params as any);// as unknown as HttpRequest

        const signer = new SignatureV4({
            credentials: {
                accessKeyId: this.accessKey,
                secretAccessKey: this.secretKey,
            },
            region: this.API_REGION,
            service: "apigateway",
            sha256: Sha256,
            // utf8Decoder: fromUtf8,
        });


        const signedRequest = await signer.sign(request);
        console.log(signedRequest)

        return {...signedRequest, clone: ()=> {}} as HttpRequest
    }

    protected async fetch(params: ServiceFetchParams): Promise<any> {
        const sigv4 = await this.genAWSSig4(params)

        return super.fetch({
            ...params,
            headers: {
                ...params.headers,
                'X-Amz-Date': '20220425T123600Z',
                ...sigv4.headers
            }
        })
    }

}
