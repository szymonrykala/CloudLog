import { Close } from "@mui/icons-material"
import { Alert, IconButton } from "@mui/joy"
import { useState, useEffect } from "react"



export default function ErrorBanner(props: { message: string | null }) {
    const [message, setMessage] = useState<string>(props.message || "")

    useEffect(() => {
        setMessage(String(props.message))
    }, [props.message])

    return <>
        {
            Boolean(message) ?
                <Alert color="warning" variant="soft"
                    endDecorator={
                        <IconButton onClick={() => setMessage('')} color="warning" variant="outlined">
                            <Close />
                        </IconButton>
                    }
                >
                    {message}
                </Alert>
                :
                null
        }
    </>
}