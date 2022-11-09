import Head from 'next/head'
import Header from './Header'
import Footer from './Footer'

export default function Layout({title, children}) {
  return (
    <div>
      <Head>
        <title>{title}</title>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="Brownfields in the city"
          content="Elektronický zoznam hnedých fľakov na mape"
        />
        <meta name='keywords' content="Some keywords"/>
        <meta name='description' content="Some description"/>
      </Head>
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  )
}
