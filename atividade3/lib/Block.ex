defmodule Atividade3.Block do
  # struct do bloco
  defstruct [:data, :timestamp, :hash_anterior, :hash]

  # cria o primeiro bloco da cadeia
  def zero do
    %Atividade3.Block {
      data: "primeiro",
      hash_anterior: "primeiro_hash_da_cadeia",
      timestamp: NaiveDateTime.utc_now
    }
  end

  # constroi novo bloco a partir dos dados
  # e do hash anterior
  def new(data, hash_anterior) do
    %Atividade3.Block{
      data: data,
      hash_anterior: hash_anterior,
      timestamp: NaiveDateTime.utc_now,
    }
  end

  # checa se o bloco é valido
    def valido?(%Atividade3.Block{} = block) do
      Atividade3.Crypto.hash(block) == block.hash
    end

    def valido?(
      %Atividade3.Block{} = block,
      %Atividade3.Block{} = prev_block
    ) do
      (block.hash_anterior == prev_block.hash) && valido?(block)
    end
end
