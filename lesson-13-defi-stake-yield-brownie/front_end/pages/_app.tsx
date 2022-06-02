import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { Config, DAppProvider, Rinkeby } from "@usedapp/core"
import Head from "next/head"
import { ethers } from "ethers"
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";


const config: Config = {
  readOnlyChainId: Rinkeby.chainId,
  readOnlyUrls: {
    [Rinkeby.chainId]: new ethers.providers.InfuraProvider("rinkeby", process.env.NEXT_PUBLIC_INFURA_API_KEY)
  },
  notifications: {
    expirationPeriod: 1 * 1000,
    checkInterval: 1 * 1000
  }
}

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>lesson 13</title>
      </Head>
      <DAppProvider config={config}>
        <Component {...pageProps} />
        <ToastContainer
          position="top-center"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </DAppProvider>
    </>

  )
}

export default MyApp
