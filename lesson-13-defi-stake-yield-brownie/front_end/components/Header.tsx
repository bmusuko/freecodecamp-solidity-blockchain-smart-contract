import { Box, Button } from "@mui/material"
import { useEthers } from "@usedapp/core"

export const Header = () => {
    const { activateBrowserWallet, account, deactivate } = useEthers()

    const isConnected = account !== undefined

    return (
        <Box sx={{
            padding: "4em 0em 4em 0em",
            display: "flex",
            justifyContent: "flex-end",
            gap: "1em"

        }}>
            {
                isConnected ?
                    <Button color="primary" variant="contained" onClick={deactivate} >
                        Disconnect
                    </Button> :
                    <Button color="primary" variant="contained" onClick={activateBrowserWallet} >
                        Connect
                    </Button>
            }
        </Box>
    )
}