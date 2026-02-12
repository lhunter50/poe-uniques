import Image from "next/image";
import { compactNumber } from "@/lib/format";

type PriceLineProps = {
  value: string | number | null | undefined;
  icon: "chaos" | "divine";
};

export function PriceLine({ value, icon }: PriceLineProps) {
  if (value == null) return null;

  return (
    <div className="flex items-center justify-center gap-2 text-[#7FB6FF]">
      <span className="tabular-nums">
        {compactNumber(value)}
      </span>
          <Image
        src={`/orbs/${icon}.png`}
        alt={icon}
        width={24}
        height={24}
        className="object-contain"
      />
    </div>
  );
}
