import { ReactNode, useCallback, useEffect, useState } from "react";
import { AWSGatewayService, ACCESS_KEY, SECRET_KEY } from "../API/base";

interface ICredentialsInput {
    children: ReactNode
}

export default function CredentialsInput(props: ICredentialsInput) {
    const [credsOk, setCredsOk] = useState<boolean>(false)


    const checkCredentials = useCallback(() => {
        const localAccessKey = localStorage.getItem(ACCESS_KEY)
        const localSecretKey = localStorage.getItem(SECRET_KEY)

        if (!localAccessKey || !localSecretKey) {
            let accessKey, secretKey = null

            do {
                accessKey = prompt("Insert AccessKey")
                secretKey = prompt("Insert SecretKey")
            } while (Boolean(accessKey) === false || Boolean(secretKey) === false);

            AWSGatewayService.saveCredentials(String(accessKey), String(secretKey))
            setCredsOk(true)
        } else {
            AWSGatewayService.saveCredentials(String(localAccessKey), String(localSecretKey))
            setCredsOk(true)
        }
    }, [setCredsOk])

    useEffect(() => {
        checkCredentials()
    }, [checkCredentials])

    return <>{credsOk ? props.children : null}</>
}