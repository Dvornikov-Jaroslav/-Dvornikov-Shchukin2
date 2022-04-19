def quotes(self, name):
    print(name)
    all_text = self.get_all_text(self.url)
    name = self.declination(name)
    coincidence = list()
    print(all_text)

    for elem in all_text:
        for string in elem[1]:
            for part in name:
                if part in string or part.capitalize() in string:
                    for mark in quote_marks:
                        if mark in string:
                            coincidence.append(string)
    # Убираем повторы
    itog = []
    coincidence = list(dict.fromkeys(coincidence))
    for i in range(len(coincidence)):
        coincidence[i] = coincidence[i].split('\n')
        for j in range(len(coincidence[i])):
            if name[0] in coincidence[i][j]:
                itog.append(coincidence[i][j])
    itog = set(itog)
    for elem in itog:
        print(elem)


bot.quotes('Савося') #Пример теста