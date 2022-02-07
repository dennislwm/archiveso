# Create a Lowdefy front-end for our web service

<!-- TOC -->

- [Create a Lowdefy front-end for our web service](#create-a-lowdefy-front-end-for-our-web-service)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [User Authentication](#user-authentication)
- [Deploy to Netlify](#deploy-to-netlify)
  - [Requirements](#requirements)
  - [Running on a Local Server](#running-on-a-local-server)

<!-- /TOC -->

# Constraint

Base time: 2 workday (Max: 4)

## Hill chart
```
  .
 . .
+   .
0-1-2
```

# User Authentication

To add user authentication and authorization to a Lowdefy app, you need to do the following:

* Configure an **OpenID Connect** provider, such as **Auth0**.
* Configure which pages should be public and protected.
* Add the `Login` and `Logout` actions to your app, to allow users to log in and out.

<details>
    <summary>Click here to <strong>add user authentication</strong></summary>



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
* Set your build command to `npx lowdefy@3 build-netlify`.
* Set your publish directory to `front/.lowdefy/publish`.

**Step 4**

Configure the Lowdefy server.

* Click the "**Advanced build settings**" button.
* Set the functions directory to `front/.lowdefy/functions`.

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