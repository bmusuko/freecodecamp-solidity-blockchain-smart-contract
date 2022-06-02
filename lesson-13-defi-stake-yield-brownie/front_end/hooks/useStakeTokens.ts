import { ERC20, useContractFunction, useEthers } from "@usedapp/core"
import { constants, Contract, utils } from "ethers"
import { useEffect, useState } from "react"
import TokenFarm from "../contracts/chain-info/contracts/TokenFarm.json"
import networkMapping from "../contracts/chain-info/deployments/map.json"

export const useStakeTokens = (tokenAddress: string) => {
    const { chainId } = useEthers()
    const { abi } = TokenFarm

    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero
    const tokenFarmInterface = new utils.Interface(abi)
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)

    const erc20Interface = new utils.Interface(ERC20.abi)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)

    const { send: approveERC20Send, state: approveAndStakeERC20State } = useContractFunction(erc20Contract, "approve", { transactionName: "Approve ERC20 transer" })

    const approveAndStake = (amount: string) => {
        setAmountToStake(amount)
        return approveERC20Send(tokenFarmAddress, amount)
    }

    const { send: stakeSend, state: stakeState } = useContractFunction(tokenFarmContract, "stakeTokens", { transactionName: "Stake Tokens" })

    const [amountToStake, setAmountToStake] = useState("0")

    useEffect(() => {
        if (approveAndStakeERC20State.status == "Success") {
            // stake function
            stakeSend(amountToStake, tokenAddress)
        }
    }, [approveAndStakeERC20State, tokenAddress, amountToStake])

    const [state, setState] = useState(approveAndStakeERC20State)

    useEffect(() => {
        if (approveAndStakeERC20State.status === "Success") {
            setState(stakeState)
        } else {
            setState(approveAndStakeERC20State)
        }
    }, [approveAndStakeERC20State, stakeState])

    return { approveAndStake, state }
}