import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Login() {
  const router = useRouter()
  const [username, setUsername] = useState('superadmin')
  const [password, setPassword] = useState('demoPass123')
  const [error, setError] = useState('')

  const submit = async (e:any) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/auth/login', { // proxied in dev via next.config or use full URL
        method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({username,password})
      })
      if (!res.ok) throw new Error('Login failed')
      const data = await res.json()
      // store token
      localStorage.setItem('token', data.access_token)
      router.push('/dashboard')
    } catch (err:any) {
      setError(err.message)
    }
  }

  return (
    <div style={{maxWidth:480, margin:'3rem auto'}}>
      <h1>BHUMIDRISHTI — Demo Login</h1>
      <form onSubmit={submit}>
        <div>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
        {error && <div style={{color:'red'}}>{error}</div>}
      </form>
    </div>
  )
}
