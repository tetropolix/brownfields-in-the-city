import Link from 'next/link'
import styles from '@/styles/Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <nav>
        <Link href='/'>Domov</Link>
        <Link href='list'>Vyhladávanie</Link>
        <Link href='/admin'>Admin</Link>
      </nav>
    </header>
  )
}
