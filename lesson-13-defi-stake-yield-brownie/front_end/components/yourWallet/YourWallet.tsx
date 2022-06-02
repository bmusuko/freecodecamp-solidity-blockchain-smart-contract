import { Box, Paper, Tab } from "@mui/material"
import { useState } from "react";
import { Token } from "../Main"
import TabPanel from '@mui/lab/TabPanel';
import { TabContext, TabList } from "@mui/lab";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from "./StakeForm";

interface YourWalletProps {
    supportedTokens: Array<Token>
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<string>('0');

    const handleChange = (event: React.SyntheticEvent, newValue: string) => {
        setSelectedTokenIndex(newValue);
    };
    return (
        <Paper
            elevation={12}
            sx={{
                width: '100%',
                typography: 'body1',
                background: 'white',
                borderRadius: '24px'
            }}>
            <TabContext value={selectedTokenIndex}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                    <TabList onChange={handleChange} aria-label="lab API tabs example" >
                        {
                            supportedTokens.map((token, index) => {
                                return <Tab label={token.name} value={index.toString()} key={index} />
                            })
                        }
                    </TabList>
                </Box>
                {
                    supportedTokens.map((token, index) => {
                        return <TabPanel value={index.toString()} key={index}>
                            <Box>
                                <WalletBalance token={token} />
                                <StakeForm token={token} />
                            </Box>

                        </TabPanel>
                    })
                }
            </TabContext>
        </Paper>



    )
}