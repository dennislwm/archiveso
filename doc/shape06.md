# Create a Lowdefy front-end for our web service

<!-- TOC -->

- [Create a Lowdefy front-end for our web service](#create-a-lowdefy-front-end-for-our-web-service)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Lowdefy Structure](#lowdefy-structure)
- [Deploy to Netlify](#deploy-to-netlify)
  - [Requirements](#requirements)
  - [Running on a Local Server](#running-on-a-local-server)

<!-- /TOC -->

# Constraint

Base time: 2 workday (Max: 4)

## Hill chart
```
  +
 . .
.   .
0-1-2
```

# Lowdefy Structure

A **Lowdefy** app is written as YAML files, which are combined together using the `_ref` operator when the app is built, into a configuration object that describes the entire app.

The root schema for the `lowdefy.yaml` file is:

* `lowdefy: string`: **Required** - The Lowdefy version number the app uses. This is required and cannot be reference to another file.
* `name: string`: A name for the application.
* `connections: object[]`: An array of [`connection`](https://docs.lowdefy.com/connections-and-requests) objects.
* `menus: object[]`: An array of menu objects.
* `pages: object[]`: An array of page objects.

We will keep each non-trivial objects in separate files, while using the `_ref` operator to reference these files.

* `menu-top.yaml`: An array of menu objects.
* `page-get-article.yaml`: A page object to get an article.
* `page-welcome.yaml`: A page object that is created with Lowdefy `init`.

<details>
    <summary>Click here to <strong>configure the Lowdefy app.</strong></summary>

1. Refactor the root schema. Edit the `lowdefy.yaml` file and replace the code as follows:

```yml
lowdefy: 3.23.2
name: archiveso

connections:
  - id: conn_my_api
    type: AxiosHttp
    properties:
      baseURL: https://dev.to/api

menus:
  - _ref: menu-top.yaml

pages:
  - _ref: page-get-quote.yaml
  - _ref: page-welcome.yaml
```

2. Create a file `menu-top.yaml` and add the following code:

```yml
id: menu_top
links:
  - id: menulink_get_status
    type: MenuLink
    properties:
      icon: AlertOutlined
      title: Get quote
    pageId: page_get_status
  - id: menulink_welcome
    type: MenuLink
    properties:
      icon: HomeOutlined
      title: Home
    pageId: page_welcome
```

This file exposes two menu links **Get quote** and **Home** with reference ids `menulink_get_status` and `menulink_welcome`. You can customize each [menu `icon`](https://docs.lowdefy.com/Menu#title) under `properties`.

3. Create a file `page-get-status.yaml` and add the following code:

```yml
id: page_get_status
type: PageHeaderMenu

requests:
  - id: http_get_status
    type: AxiosHttp
    connectionId: conn_my_api
    properties:
      url: /articles?top=1

events:
  onEnter:
    - id: event_get_status
      type: Request
      params: http_get_status

blocks:
  - id: md_rest_data
    type: Markdown
    properties:
      content:
        _string.concat:
          - |
            ```yaml
          - _yaml.stringify:
              - _log:
                  _request: http_get_status
          - |
            ```
```

We reference the connection object that we created in the `lowdefy.yaml` file using the `connectionId`. The request get executed on page enter, and it converts the payload from JSON to YAML format.

4. Create a file `page-welcome.yaml` and add the following code:

```yml
id: page_welcome
type: PageHeaderMenu
properties:
  title: Welcome
areas:
  content:
    justify: center
    blocks:
      - id: content_card
        type: Card
        style:
          maxWidth: 800
        blocks:
          - id: content
            type: Result
            properties:
              title: Welcome to your Lowdefy app
              subTitle: We are excited to see what you are going to build
              icon:
                name: HeartTwoTone
                color: '#f00'
            areas:
              extra:
                blocks:
                  - id: docs_button
                    type: Button
                    properties:
                      size: large
                      title: Let's build something
                      color: '#1890ff'
                    events:
                      onClick:
                        - id: link_to_docs
                          type: Link
                          params:
                            url: https://docs.lowdefy.com
                            newTab: true
  footer:
    blocks:
      - id: footer
        type: Paragraph
        properties:
          type: secondary
          content: |
            Made by a Lowdefy 🤖
```

This page is taken from the default `lowdefy.yaml` file, after we executed the `init` command.

</details>

# Deploy to Netlify

Lowdefy apps can be deployed to **Netlify**. Netlify integrates with `git` providers to automatically deploy your app when you merge changes into the main branch of your repository and deploy previews of pull requests.

<details>
    <summary>Click here to <strong>deploy to Netlify</strong></summary>

## Requirements

* [Node.js 12+](https://nodejs.org/en/download/)

## Running on a Local Server

```
npx lowdefy@latest dev --base-directory front
```

**Step 1**

Your project will need to be hosted as a **GitHub** repository.

**Step 2**

Link your GitHub project to Netlify.

* Once logged in to Netlify, click the "**New site from git**" button.
* Choose GitHub, and authorize Netlify to access your repositories.
* Select your repository.
If your repository isn't found, click "**Configure Netlify on Github**", and give Netlify access to your repository.

**Step 3**

Configure your Netlify deployment.

* Set your base directory to `front`.
* Set your build command to `npx lowdefy@latest build-netlify`.
* Set your publish directory to `front/.lowdefy/publish`.

**Step 4**

Configure the Lowdefy server.

* Click the "**Advanced build settings**" button.
* Set the functions directory to `.lowdefy/functions`.

**Step 5**

Deploy your site.

* Click "Deploy site"
On the "**Site overview**" tab you will find your site url.

**Step 6**

In your local GitHub folder, create a sub folder `front` then:

```sh
cd front
npx lowdefy@latest init
```

This will create two files, `lowdefy.yaml` and `.gitignore`, and a hidden folder `.lowdefy/` in your `front` folder. The first file is the starting point of your front end, which we will replace with our own code.