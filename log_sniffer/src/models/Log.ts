
export enum OS {
    WINDOWS = 'windows',
    LINUX = 'linux'
}


export enum Type {
    SYSTEM = 'system',
    APP = 'application',
    LOGGER = 'logger'
}


export default interface Log {
    id: string
    type: Type
    os: OS
    message: string
    hostname: string
    unit: string
    raw: string
    severity: number
    timestamp: number
}
