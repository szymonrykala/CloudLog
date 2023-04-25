import { createContext, ReactNode, useCallback, useContext, useState } from "react";


export interface IQueryParamsContext<T> {
    setParam(name: keyof T, value: any): void
    params: T
}


const QueryParamsContext = createContext({});

export const UNSET = "unset";


export interface IQueryParamsContextProvider<T> {
    defaults: T
    children: ReactNode
}


export default function QueryParamsContextProvider<T>({
    defaults,
    children
}: IQueryParamsContextProvider<T>) {
    const [params, setParams] = useState<T>(defaults)


    const setParam = useCallback((name: keyof T, value: any) => {
        const newParams = params
        console.debug(name, value)
        if (value === UNSET) {
            delete newParams[name]
        } else {
            newParams[name] = value
        }
        console.debug(newParams)
        setParams({...newParams})

    }, [setParams, params])


    return (
        <QueryParamsContext.Provider value={{
            setParam,
            params
        } as IQueryParamsContext<T>}>
            {children}
        </QueryParamsContext.Provider>
    )
}


export function useQueryParamsContext<T>() {
    return useContext(QueryParamsContext) as IQueryParamsContext<T>
}