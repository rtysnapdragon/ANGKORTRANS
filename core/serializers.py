from rest_framework import serializers


def to_pascal_case(value):

    return ''.join(
        word.capitalize()
        for word in value.split('_')
    )


class PascalCaseSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):

        data = super().to_representation(instance)

        return {
            to_pascal_case(key): value
            for key, value in data.items()
        }