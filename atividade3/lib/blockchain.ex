defmodule Atividade3.Blockchain do

  # cria uma blockchain com bloco zero

  def new do
    [Atividade3.Crypto.add_hash(Atividade3.Block.zero)]
  end

  #insere novo bloco na blockchain
  def insere(blockchain, data) when is_list(blockchain) do
    %Atividade3.Block{hash: prev} = hd(blockchain)

    block =
      data
      |> Atividade3.Block.new(prev)
      |> Atividade3.Crypto.add_hash

    [block | blockchain]
  end

  # valida a cadeia
  def valido?(blockchain) when is_list(blockchain) do
    zero = Enum.reduce_while(blockchain, nil, fn prev, current ->
      cond do
        current == nil -> {:cont, prev}
        Atividade3.Block.valido?(current, prev) -> {:cont, prev}
        true -> {:halt, false}
      end
    end)

    if zero , do: Atividade3.Block.valido?(zero), else: false
  end

end
