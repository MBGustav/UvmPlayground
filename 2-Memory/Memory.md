# Teste de Memória

Nesta etapa, quis apresentar algumas questões interessantes sobre o coco-tb. Nele, podemos iniciar a criação de módulos que servirão de interfaces para o módulo a ser testado. Isso significa que declaramos os pinos (entrada/saída) de cada módulo e, por fim, criamos questões de leitura, escrita como desejamos.

## Drivers de Comunicação
Como mencionado antes, teremos Drivers que têm diferentes papéis para o seu funcionamento. Neste exemplo, temos os seguintes:

- `OutputMonitor`: Endereçamos para a leitura dos sinais do nosso Design. Isso significa que fazemos *LEITURA* neste módulo.
- `InputDriver`: Driver que irá direcionar os sinais para o módulo em teste.

Definimos como é a dinâmica para a leitura do sinal que desejamos, como apresentado no recorte do arquivo `Drivers.py`.

```py
# Definição de envio de sinal:
async def _driver_send(self, pkg: packet_data, sync = True):
    self.bus.i_addr.value  = int(pkg.i_addr)
    self.bus.i_wr_en.value = int(pkg.i_wr_en)
    self.bus.i_data.value  = int(pkg.i_data)
    await RisingEdge(self.clk)

```

Trecho da leitura do sinal de `OutputMonitor`:
```py
    async def get_read_data(self):
        await RisingEdge(self.clk)
        raw = self.dut.o_data.value
        
        if 'x' in raw.binstr or 'z' in raw.binstr:
            return null_value32bit
        
        return int(raw)


```
Com eles, definimos o comportamento do Design e extraímos informações para corretude do sinal e assim podermos avaliar o comportamento por meio de aleatoriedade, se desejarmos.


## BONUS
E como seria se tivéssemos, por exemplo, um atraso de sinal? Temos também um modelo que lida com isso. Caso tenha interesse, ele se encontra em `delay_tb.py`