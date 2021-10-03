# noinspection PyProtectedMember
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.results import DeleteResult


class MotorClient:
    """
    Motor singleton.
    """
    __client: "MotorClient" = None

    def __new__(cls, connection_string=None, io_loop=None) -> "MotorClient":
        """

        :param connection_string: mongodb URI used by the host parameter.
        :param io_loop: Special event loop instance to use instead of default.
        """
        if cls.__client is None:
            cls.__client = object.__new__(cls)
            # noinspection PyTypeHints
            cls.__client.motor: AsyncIOMotorClient = AsyncIOMotorClient()

        return cls.__client

    def get_database(self, database: str) -> AsyncIOMotorDatabase:
        """
        Takes the name of the database and
        :param database:
        :return:
        """
        db = self.motor[database]
        return db

    async def create_collection(self, database: str, collection: str, codec_options=None, read_preference=None,
                                write_concern=None, read_concern=None, session=None):
        """
        Create a new :class:`~pymongo.collection.Collection` in this
        database.

        Only use it to specify options on creation.
        :param database: name of the database
        :param collection: name of the new collection
        :param codec_options: CodecOption() instance,
        :param read_preference: Describes how MongoDB clients route read operations to the members of a replica set.
        :param write_concern:WriteConcern() instance. Write concern describes the level of acknowledgment requested from
        MongoDB for write operations to a standalone mongod or to replica sets or to sharded clusters.
        :param read_concern: Control the consistency and isolation properties of the host_mdb_data read from replica sets and
         replica set shards.
        :param session: ~pymongo.client_session.ClientSession
        :return:
        """
        db = self.get_database(database)
        return await db.create_collection(
            collection,
            codec_options=codec_options,
            read_preference=read_preference,
            write_concern=write_concern,
            read_concern=read_concern,
            session=session)

    def get_collection(self, database_name, collection_name, codec_options=None, read_preference=None,
                       write_concern=None, read_concern=None) -> AsyncIOMotorCollection:
        db = self.get_database(database_name)
        return db.get_collection(
            collection_name,
            codec_options=codec_options,
            read_preference=read_preference,
            write_concern=write_concern,
            read_concern=read_concern,
        )

    def list_collection_names(self, database: str, session=None, _filter=None):
        """
        Get a list of all the collection names in this database.
        :param database:
        :param session: :class:`~pymongo.client_session.ClientSession`, created with :meth:`~MotorClient.start_session`
        :param _filter: A query document to filter the list of collections returned from the listCollections command.
            filter = {"name": {"$regex": r"^(?!system\.)"}}
        :return: list
        """
        db = self.get_database(database)
        return db.list_collection_names(session=session, filter=_filter)

    def collection_bulk_write(self, database_name, collection_name, requests: list, ordered=True,
                              bypass_document_validation=False, session=None):
        """
        Send a batch of WRITE operations to the server.

        :param database_name:
        :param collection_name:

        :param requests: list of write operation instances imported from pymongo.
            :class:`~pymongo.operations.InsertOne`
            :class:`~pymongo.operations.UpdateOne`
            :class:`~pymongo.operations.UpdateMany`
            :class:`~pymongo.operations.ReplaceOne`
            :class:`~pymongo.operations.DeleteOne`
            :class:`~pymongo.operations.DeleteMany`

            For example, say we have these documents::

            {'x': 1, '_id': ObjectId('54f62e60fba5226811f634ef')}
            {'x': 1, '_id': ObjectId('54f62e60fba5226811f634f0')}

            We can insert a document, delete one, and replace one like so::

            # DeleteMany, UpdateOne, and UpdateMany are also available.
            from pymongo import InsertOne, DeleteOne, ReplaceOne

            async def modify_data():
                requests = [
                    InsertOne({'y': 1}),
                    DeleteOne({'x': 1}),
                    ReplaceOne({'w': 1}, {'z': 1}, upsert=True)
                    ]

                result = await db.test.bulk _write(requests) print("inserted %d, deleted %d, modified %d" % (
                result.inserted_count, result.deleted_count, result.modified_count)) print("upserted_ids: %s" %
                result.upserted_ids) print("collection:")

            async for doc in db.test.find():
                print(doc)

            This will print something like::

            inserted 1, deleted 1, modified 0
            upserted_ids: {2: ObjectId('54f62ee28891e756a6e1abd5')}

            collection:
            {'x': 1, '_id': ObjectId('54f62e60fba5226811f634f0')}
            {'y': 1, '_id': ObjectId('54f62ee2fba5226811f634f1')}
            {'z': 1, '_id': ObjectId('54f62ee28891e756a6e1abd5')}

        :param ordered: (optional): If ``True`` (the default) requests will be
            performed on the server serially, in the order provided. If an error
            occurs all remaining operations are aborted. If ``False`` requests
            will be performed on the server in arbitrary order, possibly in
            parallel, and all operations will be attempted.

        :param bypass_document_validation: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.

        :param session: a
            :class:`~pymongo.client_session.ClientSession`, created with
            :meth:`~MotorClient.start_session`.

        :return: An instance of :class:`~pymongo.results.BulkWriteResult`.
        """
        collection = self.get_collection(database_name, collection_name)
        collection.collection_bulk_write(
            requests=requests,
            ordered=ordered,
            bypass_document_validation=bypass_document_validation,
            session=session
        )

    def count_documents(self, database_name, collection_name, _filter, session=None):
        """
        Count the number of documents for collection in database.

        .. note::
            For a fast count of the total documents in a collection see
            :meth:`estimated_document_count`.

        The :meth:`count_documents` method is supported in a transaction.

        All optional parameters should be passed as keyword arguments
        to this method. Valid options include:

            - `skip` (int): The number of matching documents to skip before
            returning results.
            - `limit` (int): The maximum number of documents to count. Must be
            a positive integer. If not provided, no limit is imposed.
            - `maxTimeMS` (int): The maximum amount of time to allow this
            operation to run, in milliseconds.
            - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
            - `hint` (string or list of tuples): The index to use. Specify either
            the index name as a string or the index specification as a list of
            tuples (e.g. [('a', pymongo.ASCENDING), ('b', pymongo.ASCENDING)]).
            This option is only supported on MongoDB 3.6 and above.

        The :meth:`count_documents` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        :Parameters:
            - `_filter` (required): A query document that selects which documents
            to count in the collection. Can be an empty document to count all
            documents.
            - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
            - `**kwargs` (optional): See list of options above.
        """
        collection = self.get_collection(database_name, collection_name)
        return collection.count_documents(filter=_filter, session=session)

    def delete_many_documents(self, database_name, collection_name, _filter, collation=None, hint=None,
                              session=None) -> DeleteResult:
        """
        Delete one or more documents matching the filter.

        If we have a collection with 3 documents like ``{'x': 1}``, then::
            async def clear_collection():
                result = await db.test.delete_many({'x': 1})
                print(result.deleted_count)

        This deletes all matching documents and prints "3".

        :Parameters:
        - `filter`: A query that matches the documents to delete.

        - `collation` (optional): An instance of
        :class:`~pymongo.collation.Collation`. This option is only supported
        on MongoDB 3.4 and above.

        - `hint` (optional): An index used to support the query predicate specified
        either by its string name, or in the same format as passed to
        :meth:`~MotorDatabase.create_index` (e.g. ``[('field', ASCENDING)]``).
        This option is only supported on MongoDB 4.4 and above.

        - `session` (optional): a
        :class:`~pymongo.client_session.ClientSession`, created with
        :meth:`~MotorClient.start_session`.

        :Returns:
        - An instance of :class:`~pymongo.results.DeleteResult`.
        """
        collection = self.get_collection(database_name, collection_name)
        return collection.delete_many(_filter, collation=collation, hint=hint, session=session)
