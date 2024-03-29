import { Box, Chip, ColorPaletteProp, Divider, IconButton, Link, ListItem, ListItemContent, Sheet, Stack, Typography } from "@mui/joy";
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import React from "react";
import Log from "../../models/Log";
import { coloredSeverities } from "../../models/data"
import { useQueryParamsContext } from "../QueryParams/context";
import { GetLogsQueryParams } from "../../API/cloudlog";


interface ICollapsibleListItem {
    log: Log,
    open?: boolean,
}

function displayRawLog(rawLog: string): string {
    try {
        const loaded = JSON.parse(rawLog)
        return JSON.stringify(loaded, null, 4)
    } catch (e) {
        return rawLog
    }
}


export default function LogListItem(props: ICollapsibleListItem) {
    const [open, setOpen] = React.useState<boolean>(Boolean(props.open));
    const { setParam } = useQueryParamsContext<GetLogsQueryParams>();
    const log = props.log

    return (
        <>
            <ListItem sx={{
                bgcolor: "background.componentBg"
            }}>
                <ListItemContent>

                    <Stack direction="row" spacing={1} alignItems="center">
                        <IconButton
                            size="md"
                            variant="plain"
                            onClick={() => setOpen(!open)}
                        >
                            {
                                open ?
                                    <ArrowDropDownIcon color="primary" />
                                    : <ArrowRightIcon />
                            }
                        </IconButton>

                        <Stack direction="column" spacing={1}>
                            <Stack direction="row" spacing={1} flexWrap="wrap" justifyContent="flex-start" alignItems={"baseline"} >

                                {
                                    [
                                        new Date(log.timestamp * 1000).toISOString(),
                                        <Chip component='span' size="md" variant="soft" color={coloredSeverities[log.severity].color as ColorPaletteProp}>
                                            {coloredSeverities[log.severity].name.toUpperCase()}
                                        </Chip>,
                                        log.type.toUpperCase(),
                                        <Link sx={{ overflowWrap: "anywhere" }} color="neutral" onClick={() => setParam('hostname', log.hostname)}>{log.hostname}</Link>,
                                        <Link sx={{ overflowWrap: "anywhere" }} color="neutral" onClick={() => setParam('unit', log.unit)}>{log.unit}</Link>,
                                    ].map((text, id) =>
                                        <Typography
                                            key={id} level="body2"
                                            minWidth={180}
                                            // width="10%"
                                            // maxWidth={150}
                                            textOverflow={"clip"}
                                            sx={{ wordWrap: "break-word" }}
                                        >
                                            {text}
                                        </Typography>)
                                }
                            </Stack>

                            <Box>
                                <Typography>
                                    {log.message}
                                </Typography>

                            </Box>
                            {open && <Divider/>}
                        </Stack>
                    </Stack>
                </ListItemContent>
            </ListItem>

            <ListItem nested sx={{
                display: open ? 'flex' : 'none',
                bgcolor: "background.componentBg",
                marginTop: -1
            }}>
                <ListItemContent>
                    <Sheet sx={{ ml: 6, fontSize: 14, bgcolor: 'inherit' }}>
                        <Typography fontSize='inherit'>
                            Raw content:
                        </Typography>
                        <Typography fontSize='inherit' component="pre" sx={{ overflowWrap: "break-word", whiteSpace: "break-spaces", wordBreak: "break-all" }}>
                            {displayRawLog(log.raw)}
                        </Typography>
                    </Sheet>
                </ListItemContent>
            </ListItem>
        </>
    )
}


