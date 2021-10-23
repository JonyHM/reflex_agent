class Helper:
        
  def getNumberInput(self, options, inputTitle='Selecione a opção do menu: '):
    inputValue = input(inputTitle)

    try:
      inputValue = int(inputValue)
      if inputValue <= len(options):
        return inputValue
      print('Opção inválida! Tente novamente')
    except:
      print('Opção inválida! Tente novamente')

    return self.getNumberInput(options, inputTitle)