import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
    try {
        const requestUrl = new URL(request.url)
        const code = requestUrl.searchParams.get('code')

        if (code) {
            const cookieStore = cookies()
            const supabase = createRouteHandlerClient({ cookies: () => cookieStore })

            const { data: { session }, error } = await supabase.auth.exchangeCodeForSession(code)

            if (error) {
                console.error('Auth error:', error)
                return NextResponse.redirect(new URL('/auth', request.url))
            }

            if (session) {
                // Set the auth cookie
                const response = NextResponse.redirect(new URL('/dashboard', request.url))
                response.cookies.set('sb-access-token', session.access_token, {
                    path: '/',
                    httpOnly: true,
                    secure: process.env.NODE_ENV === 'production',
                    sameSite: 'lax',
                })
                response.cookies.set('sb-refresh-token', session.refresh_token!, {
                    path: '/',
                    httpOnly: true,
                    secure: process.env.NODE_ENV === 'production',
                    sameSite: 'lax',
                })
                return response
            }
        }

        return NextResponse.redirect(new URL('/auth', request.url))
    } catch (error) {
        console.error('Callback error:', error)
        return NextResponse.redirect(new URL('/auth', request.url))
    }
} 