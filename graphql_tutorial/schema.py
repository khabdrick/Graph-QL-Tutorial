import graphene
from graphene_django import DjangoObjectType #used to change Django object into a format that is readable by GraphQL
from app.models import Contact

class ContactType(DjangoObjectType):
    # Decribe the data that sre to be formatted into GraphQL fields
    class Meta:
        model = Contact
        field = ("id", "name", "phone_number")

class Query(graphene.ObjectType):
    #query ContactType to get list of contacts
    list_contact=graphene.List(ContactType)
    read_contact = graphene.Field(ContactType, id=graphene.Int()) # id=graphene.Int() gives id an integer datatype

    def resolve_list_contact(root, info):
        # We can easily optimize query count in the resolve method
        return Contact.objects.all()
    def resolve_read_contact(root, info, id):
        # get data where id in the database = id queried from the frontend
        return Contact.objects.get(id=id)

class ContactMutation(graphene.Mutation):
    class Arguments:
        # add fields you will like to create. This will corelate with the ContactType fields above
        id = graphene.ID() # new
        name=graphene.String()
        phone_number=graphene.String()
    contact = graphene.Field(ContactType) # define the class we are getting the fields from
    
    @classmethod
    def mutate(cls, root, info, name, phone_number, id):
        # function that will save the data
       ###########Create##############
        contact = Contact(name=name, phone_number=phone_number) #accepts all fields
        contact.save() #save the contact

       ########Update##############
        get_contact = Contact.objects.get(id=id)
        get_contact.name = name #override name
        get_contact.phone_number = phone_number #override phone_number
        get_contact.save()

class ContactDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    contact = graphene.Field(ContactType)
 
    @classmethod   
    def mutate(cls, root, info, id):
        contact = Contact(id=id) 
        #########Delete##############
        contact.delete()

class Mutation(graphene.ObjectType):
    create_contact = ContactMutation.Field()  
    update_contact = ContactMutation.Field() #new
    delete_contact = ContactDelete.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)