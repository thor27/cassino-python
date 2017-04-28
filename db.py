import motor.motor_asyncio


class PollDB(object):
    def __init__(self, mongo_url='mongodb://localhost:27017/'):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        self.db = self.client['cassino']
        self.collection = self.db['result']

    async def create(self, data):
        result = await self.collection.insert_one({
            "resourceId": data['resourceId'],
            "values": dict([(str(x),0) for x in range(data['numOptions'])])
        })

    async def update(self, data):
        print('Bulk Insert: ', data)
        for resourceId in data:
            values = self._translate_data_update(data[resourceId])
            result = await self.collection.update_one(
                {"resourceId": resourceId},
                {"$inc": values}
            )

    def _translate_data_update(self, data):
        return dict([("values."+str(x), data[x]) for x in data])


db = PollDB()
