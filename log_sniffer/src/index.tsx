import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { CssVarsProvider } from '@mui/joy/styles/CssVarsProvider';
import StyledEngineProvider from '@mui/joy/styles/StyledEngineProvider';
import GlobalStyles from '@mui/joy/GlobalStyles';
import appTheme from "./theme"


const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <>
    {/* <React.StrictMode> */}
    <StyledEngineProvider injectFirst>

      <CssVarsProvider disableTransitionOnChange theme={appTheme}>
        <GlobalStyles
          styles={(theme) => ({
            body: {
              margin: 0,
              fontFamily: theme.vars.fontFamily.body,
            },
          })}
        />
        <App />
      </CssVarsProvider>
    </StyledEngineProvider>
    {/* </React.StrictMode> */}
  </>
);
