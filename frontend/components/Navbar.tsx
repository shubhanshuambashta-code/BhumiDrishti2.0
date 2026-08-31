import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Navbar(){
  const [notifications, setNotifications] = useState<any[]>([])
  const [count, setCount] = useState<number>(0)
  const [open, setOpen] = useState(false)

  useEffect(()=>{ loadNotifications() },[])

  const loadNotifications = async ()=>{
    const token = localStorage.getItem('token')
    const res = await fetch('/api/notifications?unread_only=true', {headers:{'Authorization': `Bearer ${token}`}})
    const d = await res.json()
    setNotifications(d.rows || [])
    setCount(d.total || 0)
  }

  const markRead = async (id:number)=>{
    const token = localStorage.getItem('token')
    await fetch(`/api/notifications/${id}/read`, {method:'POST', headers:{'Authorization': `Bearer ${token}`}})
    loadNotifications()
  }

  return (
    <header className="flex items-center justify-between py-4">
      <div className="flex items-center">
        <Link href="/"><a className="text-xl font-semibold">BHUMIDRISHTI</a></Link>
      </div>
      <nav className="flex items-center space-x-4">
        <Link href="/map"><a className="text-indigo-600">Map</a></Link>
        <Link href="/alerts"><a className="text-indigo-600">Alerts</a></Link>
        <Link href="/tasks"><a className="text-indigo-600">Tasks</a></Link>
        <div className="relative">
          <button onClick={()=>setOpen(!open)} className="relative">
            Notifications
            {count>0 && <span className="ml-2 inline-block bg-red-600 text-white text-xs px-2 py-0.5 rounded-full">{count}</span>}
          </button>
          {open && (
            <div className="absolute right-0 mt-2 w-80 bg-white shadow rounded">
              <div className="p-2">
                <h4 className="font-semibold">Notifications</h4>
                {notifications.length===0 && <div className="text-sm text-gray-500">No unread notifications</div>}
                {notifications.map(n=> (
                  <div key={n.id} className="border-b py-2">
                    <div className="text-sm">{n.message}</div>
                    <div className="text-xs text-gray-500">{n.created_at}</div>
                    <div className="mt-1">
                      <button onClick={()=>markRead(n.id)} className="text-sm text-indigo-600">Mark read</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </nav>
    </header>
  )
}
