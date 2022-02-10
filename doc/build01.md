# Lowdefy user authentication

<!-- TOC -->

- [Lowdefy user authentication](#lowdefy-user-authentication)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Requirements](#requirements)
- [Configure the Lowdefy environment](#configure-the-lowdefy-environment)
- [Modify Lowdefy root schema](#modify-lowdefy-root-schema)
- [Build Lowdefy action pages](#build-lowdefy-action-pages)
- [Build Lowdefy reusable components](#build-lowdefy-reusable-components)
- [Build a Javascript login script](#build-a-javascript-login-script)
- [Create a MongoDB cluster](#create-a-mongodb-cluster)
- [Create an Auth0 OpenID Connect provider](#create-an-auth0-openid-connect-provider)
- [Secure the Auth0 connections](#secure-the-auth0-connections)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 .
. +
0-1
```

# Requirements

To add user authentication to a Lowdefy app, you need to do the following:

- Configure an OpenID Connect provider.
- Configure a MongoDB cluster.
- Configure the Lowdefy environment.
- Add the `404` page for **Not Found** and to enable user to navigate home.
- Add the `Logout` context action.
- Add the `Login` context action.
- Add the `User Profile` page to enable user to logout.
- Add the `Avatar` component box to show user status.
- Add the `loginRule.js` functions to interact with the OpenID Connect provider.

# Configure the Lowdefy environment

1. Create a JSON web token secret

```sh
node -e "console.log(require('crypto').randomBytes(256).toString('base64'));"
```

Your Lowdefy app uses this secret to sign the tokens used to authorize users. Copy down the generated `YOUR_SECRET_KEY`.

2. Create a `.env` file in the path `front/`, and add the following:

```
LOWDEFY_SECRET_MONGODB_URI = YOUR_MONGODB_CONNECTION_STRING
LOWDEFY_SECRET_OPENID_CLIENT_ID = YOUR_AUTHO_CLIENT_ID
LOWDEFY_SECRET_OPENID_CLIENT_SECRET = YOUR_AUTHO_CLIENT_SECRET
LOWDEFY_SECRET_OPENID_DOMAIN = YOUR_AUTHO_DOMAIN
LOWDEFY_SECRET_JWT_SECRET = YOUR_SECRET_KEY
```

# Modify Lowdefy root schema

1. Edit the file `lowdefy.yaml` in the path `front/`. Insert the following code:

```yml
lowdefy: 3.23.2
...
config:
  # Always direct users to the login page, which will redirect them to the correct page.
  homePageId: page_login
  auth:
    openId:
      # Logout redirect URI for Auth0
      logoutRedirectUri: '{{ openid_domain }}/v2/logout?returnTo={{ host }}/logged-out&client_id={{ client_id }}'
    pages:
      # All pages in the app can be seen only by logged in users
      protected: true
      # except for the following pages:
      public:
        - '404'
        - logged-out
        - page_login
...
pages:
  - _ref: pages/404.yaml
  - _ref: pages/page-get-status.yaml
  - _ref: pages/page-logged-out.yaml
  - _ref: pages/page-login.yaml
  - _ref: pages/page-profile.yaml
  - _ref: pages/page-post-url.yaml
```

# Build Lowdefy action pages

1. Create a file `404.yaml` in the path `front/pages/`. Enter the following code:

```yml
id: '404'
type: Context

blocks:
  - id: result_404
    type: Result
    properties:
      status: 404
      title: '404'
      subTitle: Sorry, the page you are visiting does not exist.
    areas:
      extra:
        blocks:
          - id: home
            type: Button
            properties:
              title: Go to home page
              type: Link
              icon: HomeOutlined
            events:
              onClick:
                - id: home
                  type: Link
                  params:
                    home: true
```

2. Create a file `page-logged-out.yaml` in the path `front/pages`. Enter the following code:

```yml
# This page is public.
# Users are redirected to this page after they have been logged out from Auth0.
# This is configured at "config.auth.openId.logoutRedirectUri" in the Lowdefy configuration,
# This page needs to be configured as an "Allowed Logout URL" in the Auth0 application.
# Alternatively, the could be redirected to the Lowdefy "login" page, which will redirect them back to the
# Auth0 login page.

# Unlike other pages, the id for this page is a keyword and cannot be changed.
id: logged-out
type: Context

layout:
  contentGutter: 16
  contentJustify: center
properties:
  title: Logged Out
events:
  onEnter:
    #
    - id: logged_in_redirect
      type: Link
      skip:
        _eq:
          - _user: sub
          - null
      params: page_post_url
blocks:
  - id: box
    type: Box
    layout:
      contentAlign: center
      contentGutter: 20
      size: 800
    style:
      margin: 100px 20px
    blocks:
      - id: logo
        type: Html
        style:
          textAlign: center
        properties:
          html: |
            <img style="width: 80%; max-width: 250px;" src="/public/logo-light-theme.png" alt="Logo"/>
      - id: login_button
        type: Button
        style:
          margin: 40px
          maxWidth: 300
        properties:
          title: Login
          icon: LoginOutlined
          size: large
          block: true
          shape: round
          type: primary
        events:
          onClick:
            - id: login
              type: Login
              params:
                pageId: page_post_url
```

3. Create a file `page-login.yaml` in the path `front/pages/`. Enter the following code:

```yml
# This page is public
# If the user is logged in, this page will redirect to the "protected-page" page.
# If the user is not logged in, it will call the Login action, which redirects the user
# to the OpenID Connect provider's login page.
id: page_login
type: Context

layout:
  contentGutter: 16
  contentJustify: center
properties:
  title: Login
events:
  onEnter:
    # Redirect to "protected-page" if user is already logged in.
    - id: logged_in_redirect
      type: Link
      skip:
        _eq:
          - _user: sub
          - null
      params: page_post_url
    # Call the Login action to log the user in.
    - id: login
      type: Login
      skip:
        _ne:
          - _user: sub
          - null
      params:
        # Redirect to "protected-page" after login is complete.
        pageId: page_post_url
```

4. Create a file `page-profile.yaml` in the path `front/pages/`. Enter the following code:

```yml
# This page is protected, so can only be accessed by logged in users.
# You don't need a role to view this page.
id: page_profile
type: PageHeaderMenu

properties:
  title: Profile
  # Prefetch the "edit-profile" page, since it is likely that the user will navigate there.
  prefetchPages:
    - edit-profile
layout:
  contentJustify: center
areas:
  header:
    blocks:
      - _ref: components/user-avatar.yaml

blocks:
  - id: title
    type: Title
    style:
      textAlign: center
    properties:
      content: Profile
      level: 2
  - id: content_card
    type: Card
    layout:
      size: 600
      contentGutter: 16
      contentJustify: center
    blocks:
      # Display all the user details.
      - id: avatar
        type: Avatar
        layout:
          size: auto
        properties:
          size: 120
          src:
            _user: picture
          alt:
            _user: name
      - id: details
        type: Descriptions
        properties:
          column: 1
          items:
            - label: Email
              value:
                _user: email
      # A button to call the "Logout" action.
      # The "Logout" action will clear the user data and authorization cookie in the lowdefy app,
      # and then redirect to the URL specified at "config.auth.openId.logoutRedirectUri"
      # in the Lowdefy configuration.
      # This URL is configured to be the logout URL for Auth0, which will logout the user from Auth0, and then to redirect the user back to the "logged-out" Lowdefy app after logging out.
      - id: btn_logout
        type: Button
        layout:
          span: 12
        properties:
          title: Logout
          icon: LogoutOutlined
          type: default
          block: true
        events:
          onClick:
            - id: logout
              type: Logout
```

# Build Lowdefy reusable components

1. Create a file `user-avatar.yaml` in the path `front/components/`. Enter the following code:

```yml
# The user avatar allows users to login, logout, and view and edit their profile.
id: user_avatar
type: Box

blocks:
  # Show a login button if the user is not logged in.
  - id: user_avatar_login_button
    type: Button
    visible:
      _eq:
        - _user: sub
        - null
    properties:
      type: default
      shape: round
      title: Login
      icon: LoginOutlined
    events:
      onClick:
        - id: login
          type: Login
  # Show the user name and avatar if the user is logged in.
  # Clicking on this Box will link to the "profile" page.
  - id: user_profile_link
    type: Box
    visible:
      _ne:
        - _user: sub
        - null
    layout:
      contentGutter: 8
      contentAlign: middle
    style:
      marginTop: 8
    events:
      onClick:
        - id: link_to_profile
          type: Link
          params: page_profile
    blocks:
      - id: user_name
        type: Html
        layout:
          flex: 0 1 auto
        # Only show the name if the screen width is greater that 992px
        visible:
          _gt:
            - _media: width
            - 992
        style:
          color: white
        properties:
          html:
            # Show the user name using the "name" claim on the user object/OpenID Connect ID token.
            _user: name
        # Show the user avatar using the "picture" claim on the user object/OpenID Connect ID token.
      - id: user_avatar
        type: Avatar
        layout:
          flex: 0 1 auto
        properties:
          size: large
          src:
            _user: picture
          alt:
            _user: name
```

# Build a Javascript login script

1. Create a `loginRule.js` file in the path `front/auth0/`. Enter the following code:

```js
/*
  This login rule enforces a "invite-only" user system
*/

async function loginRule(user, context, callback) {
  const MongoClient = require('mongodb@3.1.4').MongoClient;
  // Namespace for custom claims
  // See: https://auth0.com/docs/tokens/create-namespaced-custom-claims
  const namespace = 'https://example.com';
  try {

    // Check if the user logged in with an email.
    if (!user.email) throw new UnauthorizedError('Access denied.');

    // The MongoDB connection is memoized in global, so it can be reused.
    // If it does not exist, it is created and stored.
    if (!global.userCollection) {
      const client = new MongoClient(configuration.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
      });
      try {
        await client.connect();
        const userCollection = client.db().collection('users');
        global.userCollection = userCollection;
      } catch (error) {
        await client.close();
        throw error;
      }
    }

    // Find the user in MongoDB by email
    // convert emails to lowercase so they are not case sensitive.
    const foundUser = await global.userCollection.findOne({
      $expr: { $eq: [user.email.toLowerCase(), { $toLower: '$email' }] },
    });

    // If the user cannot be found, the have not been authorized to acces the app.
    // Throw an UnauthorizedError to deny access.
    if (!foundUser) throw new UnauthorizedError('Access denied.');

    // Update the user profile claims based on the data in the MongoDB database.
    // These claims are maintained in MongoDB from the Lowdefy app.
    user.name = foundUser.name;
    user.given_name = foundUser.given_name;
    user.family_name = foundUser.family_name;
    user.picture = foundUser.picture;

    // Add a "roles" custom claim to the OpenID Connect ID token.
    context.idToken[`${namespace}/roles`] = foundUser.roles;

    // If it is the first time the user logs in,
    // update the user "sub" field (OpenID Connect user ID).
    if (!foundUser.sub) {
      await global.userCollection.updateOne(
        { _id: foundUser._id },
        { $set: { sub: user.user_id } }
      );
    }

    // Call the callback to indicate success
    callback(null, user, context);
  } catch (error) {
    // Call the callback with the error.
    callback(error);
  }
}
```

# Create a MongoDB cluster

<details>
    <summary>Click here to <strong>create a MongoDB cluster.</strong></summary>

1. Sign up for a free **MongoDB** account.

2. In the **Deployment** section, click **Database** --> **Create** --> **Shared**. Select a Cloud Provider & Region.

3. In the **Cluster Tier** section, select the **M0 Sandbox** free forever tier.

> Note: There is a limit of one M0 cluster per project.

4. Click **Create Cluster** button.

5. In the **Deployment** section, select your new cluster, click **Connect** --> **Connect your application**. Copy YOUR_MONGODB_CONNECTION_STRING, e.g. `mongodb+srv://<MONGODB_USERNAME>:<MONGODB_PASSWORD>@dl-google-asia-se1-m0-5.zwsqj.gcp.mongodb.net/<MONGODB_DATABASE>?retryWrites=true&w=majority`

6. In the **Security** section, click **Database Access** --> **+ Add New Database User** --> **Password**. Under the **Password Authentication** section, enter:

- MONGODB_USERNAME
- MONGODB_PASSWORD

7. Under the **Database User Privileges** section, select the **Built-in Role** as `Only read any database`.

8. Click **Add User**.

9. Substitute the user credentials that you just created in YOUR_MONGODB_CONNECTION_STRING. You can use any MONGODB_DATABASE in your connection string, as MongoDB will create a new database if it doesn't exist.

</details>    

# Create an Auth0 OpenID Connect provider

Lowdefy supports the OpenID Connect standard as a user authorization mechanism. We will be using **Auth0**, which is one of the [supported provider](https://docs.lowdefy.com/openid-connect), as it supports both GitHub and Gmail authentication.

<details>
    <summary>Click here to <strong>create an Auth0 OpenID Connect provider.</strong></summary>

1. Sign up for an [Auth0](https://auth0.com/) tenant.

2. Click on **Applications** --> **+ Create Application**.

3. Click on **Settings**, under **Basic Information** section enter the following:

- **Name**: `archiveso`

4. Copy down the following:

- **Domain**: `YOUR_AUTH0_DOMAIN`
- **Client ID**: `YOUR_AUTHO_CLIENT_ID`
- **Client Secret**: `YOUR_AUTHO_CLIENT_SECRET`

5. Under **Application URIs** section enter the following:

- **Allowed Callback URLs**: `http://localhost:3000/auth/openid-callback,https://archiveso.netlify.app/auth/openid-callback`

- **Allowed Logout URLs**: `http://localhost:3000/logged-out,https://archiveso.netlify.app/logged-out`

6. Click **Save Changes** button.

</details>

# Secure the Auth0 connections

1. Enable Username-Password-Authentication

2. Create a user by sign up 

3. Disable Sign Ups