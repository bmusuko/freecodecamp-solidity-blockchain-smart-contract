import { Button, CircularProgress, Grid, Input } from "@mui/material"
import { useEthers, useNotifications, useTokenBalance } from "@usedapp/core"
import { utils } from "ethers"
import { formatUnits } from "ethers/lib/utils"
import { ChangeEvent, useEffect, useState } from "react"
import { useStakeTokens } from "../../hooks/useStakeTokens"
import { Token } from "../Main"
import { toast } from "react-toastify";


interface StakeFormProps {
    token: Token
}

export const StakeForm = ({ token }: StakeFormProps) => {
    const { address: tokenAdress, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(tokenAdress, account)
    const formattedTokenBalance = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    const { notifications } = useNotifications()

    const [amount, setAmount] = useState<number | string | Array<number | string>>(0)
    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === "" ? "" : Number(event.target.value)
        setAmount(newAmount)
        console.log(`new amount: ${newAmount}`)
    }

    const { approveAndStake, state: approveAndStakeERC20State } = useStakeTokens(tokenAdress)

    const handleStakeSubmit = () => {
        const amountInWei = utils.parseEther(amount.toString())
        return approveAndStake(amountInWei.toString())
    }

    const isMining = approveAndStakeERC20State.status === "Mining"

    useEffect(() => {
        if (notifications.filter((notification) =>
            notification.type === "transactionSucceed"
            && notification.transactionName === "Approve ERC20 transer"
        ).length > 0) {
            toast.success("Approved!")
        }

        if (notifications.filter((notification) =>
            notification.type === "transactionSucceed"
            && notification.transactionName === "Stake Tokens"
        ).length > 0) {
            toast.success("Tokens Staked!")
        }
    }, [notifications])

    return (
        <>
            <Grid
                container
                spacing={2}
                justifyContent="center"
                sx={{
                    marginTop: "1em",
                    width: "100%",
                    textAlign: 'center'
                }}>
                <Grid item>
                    <Input onChange={handleInputChange} />
                </Grid>

                <Grid item alignItems="stretch" style={{ display: "flex" }}>
                    <Button color="primary" variant="contained" onClick={handleStakeSubmit} disabled={isMining}>
                        {isMining ? <CircularProgress size={26} /> : "Stake!"}
                    </Button>
                </Grid>
            </Grid>
        </>
    )
}