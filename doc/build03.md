# Build a Lowdefy page to allow user interaction

<!-- TOC -->

- [Build a Lowdefy page to allow user interaction](#build-a-lowdefy-page-to-allow-user-interaction)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Lowdefy Guidelines](#lowdefy-guidelines)
  - [Container](#container)
  - [Input](#input)
  - [Request](#request)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 .
. +
0-1
```

# Lowdefy Guidelines

- Use a **[Container](https://docs.lowdefy.com/Card)** block to pad spaces to the left and right margins of the content.
- Use an **[Event](https://docs.lowdefy.com/events-and-actions)** block to trigger when something happens on a page, like loading a page or clicking a button.
- Use a **[Request](https://docs.lowdefy.com/connections-and-requests)** action to execute a HTTP request.
- Use a **[Validate](https://docs.lowdefy.com/blocks)** action to provide in-line validation to your inputs.
- Use an **[Operator](https://docs.lowdefy.com/operators)** keyword to react to data and inputs. Each operator expects arguments with a specific structure.
  - [`_ref`](https://docs.lowdefy.com/_ref) to reference a configuration file, in order to split the Lowdefy configuration into modular files.
  - [`_regex`](https://docs.lowdefy.com/_regex) to perform validation tests on an input.
  - [`_request`](https://docs.lowdefy.com/_request) to return the response value of a request.
  - [`_string`](https://docs.lowdefy.com/_string) to manipulate strings.

## Container

Without a container block, your inputs will span the entire width of the page. You should use a **Card** container as it places blocks on a white background with a card border.

1. Create a file `page-post-url.yaml` in the path `front/pages/`. Add the following code:

```yml
id: page_post_url
type: PageHeaderMenu

properties:
  title: Add URL(s)
areas:
  header:
    blocks:
      - _ref: components/user-avatar.yaml
  content:
    justify: center
    blocks:
      - id: card_content
        type: Card
        style:
          maxWidth: 800
        blocks:
          - id: title_main
            type: Title
            properties:
              content: Add URL
              level: 3
```

## Input

1. Add a **TextArea** input under `blocks` section of the **Card** container in the same file as above:

```yml
areas:
  ...
  content:
    ...
    blocks:
      - id: card_content
        ...
        blocks:
          ...
          - id: textarea_url
            type: TextArea
            required: true
            validate:
              - message: Please provide a valid URL.
                status: error
                pass:
                  _regex: https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)
            properties:
              allowClear: true
              autoFocus: true
              autoSize: true
              label:
                title: URL(s) separated by spaces
```

The **Validate** action should be placed at the same level as the input. The schema for a validation:
- `pass: boolean`: **Required** - The test that validates if this item passes or not. This is usually written as operators which evaluates to a `true` or `false`.
- `message: string`: **Required** - The feedback message to the user if the validation fails.
- `status: enum`: Option are `error` and `warning`. Default is `error`.

2. Add a **TextArea** input under `blocks` section of the **Card** container in the same file as above:

```yml
areas:
  ...
  content:
    ...
    blocks:
      - id: card_content
        ...
        blocks:
          ...
          - id: textarea_url
            ...
          - id: button_submit
            type: Button
            style:
              marginTop: 8
            layout:
              span: 6
            properties:
              size: large
              shape: round
              title: Add
              type: primary
              block: true
            events:
              # issue: validate a single input doesn't appear to work
              onClick:
                - id: action_validate_all
                  type: Validate
                - id: action_request
                  type: Request
                  params: http_get_status
                - id: action_reset
                  type: Reset
                - id: action_message
                  type: Message
```

The `onClick` event block executes when the **Button** is clicked. It executes a sequence of tasks, and stops if any of the task fails.

3. Edit the root schema `lowdefy.yaml` in the path `front/`. Append the following code under the `pages` block:

```yml
...
pages:
  ...
  - _ref: pages/page-post-url.yaml
```

## Request

As we may reuse the **Request** action in one or more pages, we create a separate file for each request in the path `front/components/`:
- `request-get-status.yaml`
- `request-post-url.yaml`

A request action requires a **Connection** object, such as `AxiosHttp`. You reference your connection by passing the `connectionId`.

The `_request` operator is usually accompanied by the **Request** id. This returns an object that allows you to use dot notation to get the data from the response, e.g. `http_get_status.data`.

1. Create a file `request-get-status.yaml` in the path `front/components/`. Add the following code:

```yml
id: http_get_status
type: AxiosHttp
connectionId: conn_my_api
properties:
  url: /
```

The response from this request is accessible with `_request: http_get_status.data`, while `_request: http_get_status.header` displays the HTTP header information.

2. Create a file `request-post-url.yaml` in the path `front/components/`. Add the following code:

```yml
id: http_post_url
type: AxiosHttp
connectionId: conn_my_api
properties:
  url: /api/archiveso
  method: post
  data:
    _state: textarea_url
```

3. Edit the file `page-get-status.yaml` in the path `front/pages`. Insert the following code at the top as follows:

```yml
id: page_get_status
type: PageHeaderMenu

requests:
  - _ref: components/request-get-status.yaml
...
```

4. Edit the file `page-post-url.yaml` in the path `front/pages`. Insert the following code at the top as follows:

```yml
id: page_post_url
type: PageHeaderMenu

requests:
  - _ref: components/request-post-url.yaml
...
```
