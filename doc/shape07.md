# Expose our web app using Cloudflare Tunnel

<!-- TOC -->

- [Expose our web app using Cloudflare Tunnel](#expose-our-web-app-using-cloudflare-tunnel)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Prerequisites](#prerequisites)
- [Deploy container on local workstation](#deploy-container-on-local-workstation)
- [Set up cloudflared](#set-up-cloudflared)
- [Run cloudflared](#run-cloudflared)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 +
. .
0-1
```

# Place, Affordance, Connection

* Places users can navigate
  * Cloudflare tunnel to Python Flask server e.g. `https://archiveso.mydomain.com`
    * Status endpoint `/`
    * Application endpoint `/api/archiveso`

* Affordance users can act
  * Test `GET https://archiveso.mydomain.com/` returns HTTP Status `200` and payload `App-version: *`
  * Test `GET https://archiveso.mydomain.com/api/archiveso` returns HTTP Status `200`.

* Connection users are taken to
  * `GET https://archiveso.mydomain.com/` --> cloudflared --> Docker --> `main.py` --> HTTP response
  * `GET https://archiveso.mydomain.com/api/archiveso` --> cloudflared --> Docker --> `main.py` --> `clsArchiveso.py` --> `/path/to/archivebox` --> `archivebox.cli.list()` --> String --> HTTP response

# Prerequisites

* [Cloudflare free account](https://cloudflare.com)
* [Cloudflare CLI](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide)
* [Domain name with Cloudflare DNS](https://support.cloudflare.com/hc/en-us/articles/205195708-Changing-your-domain-nameservers-to-Cloudflare)

# Deploy container on local workstation

Currently, I'm hosting the Docker container Python Flask server app on my local workstation, i.e. http://localhost:8080 and using Cloud Tunnel to access it via https://archiveso.mydomain.com.

Deploy the Docker container on your local workstation. This command pulls the image from Docker Hub if it doesn't exist.

```sh
docker run -p 8080:8080 -d --rm --name objArchiveso dennislwm/archiveso:latest
```

# Set up cloudflared

<details>
    <summary>Click here to <strong>set up cloudflared.</strong></summary>

1. Run the following command to authenticate your cloudflare account:

```sh
cloudflared tunnel login
```

This will create a certificate file `cert.pem` with your credentials in the path `~/.cloudflared`.

2. Create a tunnel

```sh
cloudflared tunnel create TUNNELNAME
```

This creates a UUID that is associated with the TUNNELNAME that you gave. At this point, no connection is active within the tunnel yet.

Verify that the TUNNELNAME has been created successfully.

```sh
cloudflared tunnel list
You can obtain more detailed information for each tunnel with `cloudflared tunnel info <name/uuid>`
ID                                   NAME              CREATED              CONNECTIONS 
6ff70722-7854-454d-aeec-793674227b0d archiveso         2022-02-08T02:36:22Z             
```

3. Create a configuration file

Create a `config.yml` file in the path `~/.cloudflared/` and add the following lines:

```yml
tunnel: 6ff70722-7854-454d-aeec-793674227b0d
credentials-file: /Users/dennislwm/.cloudflared/6ff70722-7854-454d-aeec-793674227b0d.json
warp-routing:
  enabled: true
```

4. Assign a CNAME record

Now assign a CNAME record that points traffic to your subdomain.

```sh
cloudflared tunnel route dns TUNNELNAME archiveso.mydomain.com
```

5. Reference a configuration file

When running a tunnel, make sure you specify the path to your configuration file.

```sh
cloudflared tunnel --config ~/.cloudflared/config.yml run
2022-02-08T02:57:49Z INF Starting tunnel tunnelID=6ff70722-7854-454d-aeec-793674227b0d
2022-02-08T02:57:49Z INF Version 2022.1.2
2022-02-08T02:57:49Z INF GOOS: darwin, GOVersion: go1.17.2, GoArch: amd64
2022-02-08T02:57:49Z INF Settings: map[config:/Users/dennislwm/.cloudflared/config-archiveso.yml cred-file:/Users/dennislwm/.cloudflared/6ff70722-7854-454d-aeec-793674227b0d.json credentials-file:/Users/dennislwm/.cloudflared/6ff70722-7854-454d-aeec-793674227b0d.json url:http://localhost:8080]
2022-02-08T02:57:49Z INF cloudflared will not automatically update when run from the shell. To enable auto-updates, run cloudflared as a service: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/run-tunnel/run-as-service
2022-02-08T02:57:49Z INF Generated Connector ID: 36295d2e-f14e-498e-adf0-cdf6eaacddf8
2022-02-08T02:57:49Z INF Warp-routing is enabled
2022-02-08T02:57:49Z INF Initial protocol http2
2022-02-08T02:57:49Z INF Starting metrics server on 127.0.0.1:64231/metrics
2022-02-08T02:57:49Z WRN Your version 2022.1.2 is outdated. We recommend upgrading it to 2022.2.0
2022-02-08T02:57:50Z INF Connection 936af740-d529-41ab-a031-bdf8cc98d700 registered connIndex=0 location=SIN
2022-02-08T02:57:51Z INF Connection 86654f02-25ca-4670-a2b3-e9ea7c9cb6fc registered connIndex=1 location=HKG
2022-02-08T02:57:52Z INF Connection 8879ab6d-91f5-497a-978b-827dbb7ab94a registered connIndex=2 location=SIN
2022-02-08T02:57:53Z INF Connection 4eb02cf6-d584-4407-aea9-0fa68647bebe registered connIndex=3 location=HKG
```

Verify that the tunnel is complete.

```sh
cloudflared tunnel info TUNNELNAME
```

</details>

# Run cloudflared

When you run cloudflared tunnel, it remains as a foreground service. However, you can choose to run it as a [service](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/run-tunnel/run-as-service).

```sh
cloudflared tunnel --config ~/.cloudflared/config-archiveso.yml run
```

Navigate to [Lowdefy app](https://archiveso.netlify.app/page_get_status) and you should see the following:

```yml
data: 'App-version: 0.1.0'
headers:
  alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400
  cf-cache-status: DYNAMIC
  cf-ray: 6da1b1b8ad718968-SIN
  connection: close
  content-type: text/html; charset=utf-8
  date: Tue, 08 Feb 2022 03:15:33 GMT
  expect-ct: >-
    max-age=604800,
    report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
  nel: '{"success_fraction":0,"report_to":"cf-nel","max_age":604800}'
  report-to: >-
    {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v3?s=lPy8uGW1LdlVG2x13WLRsea%2Bx%2BrFxmk7qiQIuI9PzrmqLjc1lVTPoDYAEhCd014Ech858aOoGwZTGfBOI0S0Ytokb5jlRlwIyTr4lEuG9lLDmU6JMP%2Fx7FYMnx6RrBxzYOEd1SIU3GM%3D"}],"group":"cf-nel","max_age":604800}
  server: cloudflare
  transfer-encoding: chunked
status: 200
statusText: OK
```