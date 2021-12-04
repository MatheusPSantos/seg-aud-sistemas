defmodule Atividade2 do

  use Application

  def start(_type, _args) do

    children = [
      Plug.Cowboy.child_spec(
        scheme: :http,
        plug: Atividade2.Router,
        options: [
          dispatch: dispatch(),
          port: 3333
        ]
      ),
      Registry.child_spec(
        keys: :duplicate,
        name: Registry.Atividade2
      )
    ]

    opts = [strategy: :one_for_one, name: Atividade2.Application]
    Supervisor.start_link(children, opts)
  end

  defp dispatch do
    [{:_, [
      {"/ws/[..]", Atividade2.SocketHandler, []},
      {:_, Plug.Cowboy.Handler, { Atividade2.Router, [] }}
    ]}]
  end

end
