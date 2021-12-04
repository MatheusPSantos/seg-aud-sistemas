defmodule Atividade2.Router do

  use Plug.Router
  require EEx

  plug Plug.Static,
    at: "/",
    from: :atividade_2

  plug :match

  plug Plug.Parsers,
    parsers: [:json],
    pass: ["application/json"],
    json_header: Jason

  plug :dispatch

  EEx.function_from_file(:defp, :application_html, "lib/application.html.eex", [])

  get "/" do
    send_resp(conn, 200, application_html())
  end

  match _ do
    send_resp(conn, 404, "404")
  end
end
