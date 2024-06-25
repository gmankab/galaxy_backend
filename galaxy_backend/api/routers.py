from fastapi import APIRouter

coin = APIRouter(prefix='/coin')
clan = APIRouter(prefix='/clan')
clan_member = APIRouter(prefix='/clan/member')
sector = APIRouter(prefix='/sector')
planet = APIRouter(prefix='/planet')
ref = APIRouter(prefix='/ref')

