import Sheet from "@mui/joy/Sheet/Sheet";
import Stack from "@mui/joy/Stack/Stack";
import Typography from "@mui/joy/Typography/Typography";
import { UNSET, useQueryParamsContext } from "./context";
import { GetLogsQueryParams } from "../../API/cloudlog";
import Select from "@mui/joy/Select/Select";
import Option from "@mui/joy/Option/Option";
import { Type } from "../../models/Log";
import { Chip, ChipDelete, Input } from "@mui/joy";
import { severities } from "../../models/data"


export default function ParameterPanel() {
    const { setParam, params } = useQueryParamsContext<GetLogsQueryParams>()

    return (
        <Sheet
            sx={{
                padding: 1,
                gap: 3,
                display: 'flex',
                flexDirection: "column",
                alignItems: 'flex-start',
                bgcolor: 'background.componentBg',
                borderRadius: 2
            }}
        >
            <Stack direction='row' sx={{ alignItems: 'center', justifyContent: "space-between" }} spacing={2} flexWrap="wrap">
                <span>
                    <Typography level='body2'>
                        Type:
                    </Typography>
                    <Select
                        size="sm"
                        value={params?.type || UNSET}
                        variant="soft"
                        sx={{ minWidth: 120 }}
                        onChange={(e: any, value: string | null) => setParam("type", value)}
                    >
                        <Option value={Type.SYSTEM}>System</Option>
                        <Option value={Type.APP}>Application</Option>
                        <Option value={Type.LOGGER}>Logger</Option>
                        <Option value={UNSET}>unset</Option>
                    </Select>
                </span>
                <span>
                    <Typography level='body2'>
                        Severity:
                    </Typography>
                    <Select
                        size="sm"
                        value={params?.severity as any}
                        variant="soft"
                        sx={{ minWidth: 120 }}
                        onChange={(e: any, value: string | null) => setParam("severity", value)}
                    >
                        {
                            severities.map((name, index) =>
                                <Option key={index} value={index}>{name}</Option>
                            )
                        }
                    </Select>
                </span>

                <span>
                    <Typography level='body2'>
                        Since:
                    </Typography>
                    <Input
                        sx={{ lineHeight: 2 }}
                        type="datetime-local"
                        size="sm"
                        value={params.fromDate?.replace(/[:\d.Z]{8}$/, "")}
                        onChange={(e: any) => setParam("fromDate", e.target.value)}
                    />
                </span>

                <span>
                    <Typography level='body2'>
                        To:
                    </Typography>
                    <Input
                        sx={{ lineHeight: 2 }}
                        type="datetime-local"
                        size="sm"
                        value={params.toDate?.replace(/[:\d.Z]{8}$/, "")}
                        onChange={(e: any) => setParam("toDate", e.target.value)}
                    />
                </span>
            </Stack>
            <Stack direction="row" spacing={2}>
                {
                    params?.hostname && <span>Hostname:<Chip
                        size="md"
                        variant="soft"
                        endDecorator={<ChipDelete onDelete={() => setParam("hostname", UNSET)} />}
                    >
                        {params.hostname}
                    </Chip>
                    </span>
                }
                {
                    params?.unit && <span>Service: <Chip
                        size="md"
                        variant="soft"
                        endDecorator={<ChipDelete onDelete={() => setParam("unit", UNSET)} />}
                    >
                        {params.unit}
                    </Chip>
                    </span>
                }
            </Stack>
        </Sheet>
    )
}