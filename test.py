def getPowers(self, author, message):
        message = message.lower()
        searchterms = re.split('(?<!level)\s', message)

        print(str(author) + " is searching for powers with terms " + str(searchterms))

        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()

        embedresult.colour = usercolour
        results = ""

        for power in self.powers_info:
            matches = 0
            if " ".join(searchterms) == power['name'].lower():
                embedresult.clear_fields()
                embedresult.title = power['name']
                embedresult.add_field(
                    name=power['level'], value="\u200b", inline=False)
                desc = power['desc']
                embedresult.add_field(
                    name="Power Type:", value=power['power_type'], inline=False)

                if power['power_type'] == 'Force':
                    embedresult.add_field(
                        name="Force Alignment:", value=power['force_alignment'], inline=False)
                
                if (len(desc) <= 1000):
                        embedresult.add_field(
                            name="Description:", value=power['desc'], inline=False)
                else:
                    descarray = desc.split("\n")
                    for a in descarray:
                        if re.search('[a-zA-Z]', a):
                            if (descarray.index(a) == 0):
                                if (len(a) < 1000):
                                    embedresult.add_field(
                                        name="Description:", value=a, inline=False)
                            else:
                                if (len(a) < 1000):
                                    embedresult.add_field(
                                        name="\u200b", value=a, inline=False)
                embedresult.add_field(
                    name="Casting Time:", value=power['casting_time'], inline=False)
                embedresult.add_field(
                    name="Duration:", value=power['duration'], inline=False)
                embedresult.add_field(
                    name="Range:", value=power['range'], inline=False)
                embedresult.add_field(
                    name="Concentration:", value=power['concentration'], inline=False)

                if power['prerequisite'] != 'None':
                    embedresult.add_field(
                        name="Prerequisite:", value=power['prerequisite'], inline=False)

                embedresult.add_field(
                    name="Source:", value=power['content_source'], inline=False)
                
                return (embedresult)

            for term in searchterms:
                if term in power['name'].lower():
                    matches = matches + 1
                elif term in power['power_type'].lower():
                    matches = matches + 1
                elif term in power['force_alignment'].lower():
                    matches = matches + 1
                elif term in power['level'].lower():
                    matches = matches + 1

            if matches == len(searchterms):
                results = results+power['name']+"\n"

        if results != "":
            embedresult.clear_fields()
            if len(results) >= 1024:
                embedresult.add_field(
                    name="Results:", value="Too many results, narrow search", inline=False)
                print("Too many results to list.")
            else:
                embedresult.add_field(
                    name="Results:", value=results, inline=False)
                print("Returning matched powers!")
        else:
            embedresult.clear_fields()
            embedresult.add_field(
                name="Results:", value="No powers found.", inline=False)
            print("No powers found.")

        return embedresult
