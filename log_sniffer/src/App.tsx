import CredentialsInput from "./components/CredentialsInput";
import Header from "./components/Header";
import Layout from "./components/Layout"
import MainPanel from "./components/MainPanel";


function App() {
  return (
    <Layout.Root>
      <Layout.Header>
        <Header />
      </Layout.Header>
      <Layout.Main>
        <CredentialsInput>
          <MainPanel />
        </CredentialsInput>
      </Layout.Main>
    </Layout.Root>
  );
}

export default App;
