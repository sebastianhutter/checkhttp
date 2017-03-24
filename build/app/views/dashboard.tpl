<!doctype html>

<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>Status Page</title>

  <style>
    body {
      background-color: linen;
    }

    h1 {
      color: maroon;
      margin-left: 40px;
    }
    table {
      border-collapse: collapse;
    }

    table, th, td {
      border: 1px solid black;
      text-align: left;
      padding: 0.2em;
    }

    tr.title {
      background-color: #f0f5f5;
    }

    tr.ok {
      background-color: #64FE2E;
    }

    tr.error {
      background-color: #FE2E2E;
    }
  </style>
  </head>

  <body>
    <table>
    <tr class="title">
      <th>ID</th>
      <th>URL</th>
      <th>Status</th>
      <th>HTTP Code</th>
      <th>Last Check</th>
      <th>Last HTTP Code</th>
    </tr>
    % for e in endpoints:
    % if e.return_state():
    %   state = "OK"
    %   css_class="ok"
    % else:
    %   state = "ERROR"
    %   css_class = "error"
    % end
    <tr class="{{css_class}}">
      <td>{{e.id}}</td>
      <td><a href="{{e.url}}">{{e.url}}</a></td>
      <td>{{state}}</td>
      <td>{{e.return_status_code()}}</td>
      <td>{{e.return_status_code_time()}}</td>
      <td>{{e.return_last_status_code()}}</td>
    </tr>
    % end
    </table>
  </body>
</html>