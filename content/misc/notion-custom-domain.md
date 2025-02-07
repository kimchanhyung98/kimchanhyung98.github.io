Title: Cloudflare,Notion custom domain
Subtitle: 클라우드플레어를 이용한 노션 커스텀 도메인 설정
Category: misc
Date: 2024-05-15 00:00

## 노션 커스텀 도메인 설정

노션 커스텀 도메인을 설정할 때, 짧고 쉬운 가이드를 찾기 힘들어 간단하게 정리하였다.

![notion-publish]({static}/images/notion-publish.png)  
우선 노션 페이지를 공개(게시) 처리하고

![cloudflare-dns]({static}/images/notion-cloudflare-dns.png)  
클라우드플레어에서 DNS(CNAME) 추가 후, Worker를 생성한다.

```javascript
// notion-worker

const CUSTOM_DOMAIN = "memo.chanhyung.kim"
const SLUG_TO_PAGE = 'first-page-slug';

addEventListener('fetch', event => {
    event.respondWith(fetchAndApply(event.request))
})

const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, HEAD, POST,PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

function handleOptions(request) {
    if (request.headers.get("Origin") !== null && request.headers.get("Access-Control-Request-Method") !== null && request.headers.get("Access-Control-Request-Headers") !== null) {
        // Handle CORS pre-flight request.
        return new Response(null, {
            headers: corsHeaders
        })
    } else {
        // Handle standard OPTIONS request.
        return new Response(null, {
            headers: {
                "Allow": "GET, HEAD, POST, PUT, OPTIONS",
            }
        })
    }
}

async function fetchAndApply(request) {
    if (request.method === "OPTIONS") {
        return handleOptions(request)
    }
    let url = new URL(request.url)
    let response
    if (url.pathname.startsWith("/app") && url.pathname.endsWith("js")) {
        response = await fetch(`https://www.notion.so${url.pathname}`)
        let body = await response.text()
        try {
            response = new Response(body.replace(/www.notion.so/g, CUSTOM_DOMAIN).replace(/notion.so/g, CUSTOM_DOMAIN), response)
            // response = new Response(response.body, response)
            response.headers.set('Content-Type', "application/x-javascript")
            console.log("get rewrite app.js")
        } catch (err) {
            console.log(err)
        }
    } else if ((url.pathname.startsWith("/api"))) {
        response = await fetch(`https://www.notion.so${url.pathname}`, {
            body: request.body, // must match 'Content-Type' header
            headers: {
                'content-type': 'application/json;charset=UTF-8',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            }, method: "POST", // *GET, POST, PUT, DELETE, etc.
        })
        response = new Response(response.body, response)
        response.headers.set('Access-Control-Allow-Origin', "*")
    } else if (url.pathname === `/`) {
        let redrictUrl = `https://${CUSTOM_DOMAIN}/${SLUG_TO_PAGE}`
        return Response.redirect(redrictUrl, 301)
    } else {
        response = await fetch(`https://www.notion.so${url.pathname}${url.search}`, {
            body: request.body, // must match 'Content-Type' header
            headers: request.headers, method: request.method, // *GET, POST, PUT, DELETE, etc.
        })
    }
    return response
}

```

![cloudflare-worker]({static}/images/notion-cloudflare-worker.png)  
이제 설정한 도메인과 notion-worker를 등록하면, 해당 도메인으로 접속이 가능하다.  
