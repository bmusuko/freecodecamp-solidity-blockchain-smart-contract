import { Card, CardContent, CardMedia, Typography } from "@mui/material"
import { StaticImageData } from "next/image"

interface BalanceMsgProps {
    label: string
    amount: number
    tokenImgSrc: StaticImageData
}
export const BalanceMsg = ({ label, amount, tokenImgSrc }: BalanceMsgProps) => {

    return (
        <Card >
            <CardMedia
                component="img"
                image={tokenImgSrc.src}
                alt={label}
                sx={{
                    width: '345px',
                    margin: 'auto'

                }}
            />
            <CardContent>
                <Typography gutterBottom variant="h6" component="div" textAlign="center">
                    {label}
                </Typography>
                <Typography variant="body2" color="h3" textAlign="center" fontWeight={800}>
                    {amount}
                </Typography>
            </CardContent>
        </Card>
    )
}