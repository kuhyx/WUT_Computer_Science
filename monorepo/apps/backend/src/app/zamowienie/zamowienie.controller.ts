// src/zamowienie/zamowienie.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { ZamowienieService } from './zamowienie.service';
import { Zamowienie } from '@prisma/client';

@Controller('zamowienie')
export class ZamowienieController {
  constructor(private readonly zamowienieService: ZamowienieService) {}

  @Get()
  async findAll(): Promise<Zamowienie[]> {
    return this.zamowienieService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Zamowienie | null> {
    return this.zamowienieService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { status: string }): Promise<Zamowienie> {
    return this.zamowienieService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Zamowienie>): Promise<Zamowienie> {
    return this.zamowienieService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Zamowienie> {
    return this.zamowienieService.delete(+id);
  }
}
