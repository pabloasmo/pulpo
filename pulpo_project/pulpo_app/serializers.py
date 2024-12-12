from rest_framework import serializers
from .models import Tipo, Genero, Autor, Contenido, ListaUsuario, Comentario

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class ContenidoSerializer(serializers.ModelSerializer):
    tipo = TipoSerializer()
    generos = GeneroSerializer(many=True)
    autores = AutorSerializer(many=True)

    class Meta:
        model = Contenido
        fields = '__all__'

class ListaUsuarioSerializer(serializers.ModelSerializer):
    contenido = ContenidoSerializer()
    usuario = serializers.StringRelatedField()

    class Meta:
        model = ListaUsuario
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    contenido = ContenidoSerializer()
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Comentario
        fields = '__all__'
