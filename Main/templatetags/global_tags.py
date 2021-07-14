from Main.models import KIND
from django import template

register = template.Library()


@register.inclusion_tag('Main/topkind.html')
def get_topkind_list():
    MainKinds=KIND.objects.filter(PKID__isnull=True)
    res=[]
    for Kind in MainKinds:
        one={
            'MainKind':Kind,
        }
        subkinds=KIND.objects.filter(PKID=Kind.KID)
        one['SubKind']=subkinds
        res.append(one)
    return {'kinds': res}
