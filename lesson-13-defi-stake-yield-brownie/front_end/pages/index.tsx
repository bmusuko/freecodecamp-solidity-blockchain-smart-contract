import type { NextPage } from 'next'
import styles from '../styles/Home.module.css'
import { Header } from "../components/Header"
import { Container } from "@mui/material"
import { Main } from "../components/Main"


const Home: NextPage = () => {
  return (
    <Container maxWidth="md">
      <Header />
      <Main />
    </Container>

  )
}

export default Home
