/*
  Warnings:

  - You are about to drop the `Recencja` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[Historia_zamowienId]` on the table `Uzytkownik` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `Historia_zamowienId` to the `Uzytkownik` table without a default value. This is not possible if the table is not empty.
  - Added the required column `restauracjaId` to the `Znizka` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Uzytkownik" ADD COLUMN     "Historia_zamowienId" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "Znizka" ADD COLUMN     "restauracjaId" INTEGER NOT NULL;

-- DropTable
DROP TABLE "Recencja";

-- CreateTable
CREATE TABLE "Recenzja" (
    "id" SERIAL NOT NULL,
    "tekst" TEXT NOT NULL,
    "wartosc" INTEGER NOT NULL,
    "restauracjaId" INTEGER NOT NULL,
    "uzytkownikId" INTEGER NOT NULL,

    CONSTRAINT "Recenzja_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Uzytkownik_Historia_zamowienId_key" ON "Uzytkownik"("Historia_zamowienId");

-- AddForeignKey
ALTER TABLE "Recenzja" ADD CONSTRAINT "Recenzja_restauracjaId_fkey" FOREIGN KEY ("restauracjaId") REFERENCES "Restauracja"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Recenzja" ADD CONSTRAINT "Recenzja_uzytkownikId_fkey" FOREIGN KEY ("uzytkownikId") REFERENCES "Uzytkownik"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Uzytkownik" ADD CONSTRAINT "Uzytkownik_Historia_zamowienId_fkey" FOREIGN KEY ("Historia_zamowienId") REFERENCES "Historia_zamowien"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Znizka" ADD CONSTRAINT "Znizka_restauracjaId_fkey" FOREIGN KEY ("restauracjaId") REFERENCES "Restauracja"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
